#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
 //WINDOWS
#ifdef _WIN32
#include <windows.h>
#include <fcntl.h>
#include <io.h>
#define open _open
#define close _close
#define read _read
#define lseek _lseek
#define O_RDONLY _O_RDONLY
typedef HANDLE ThreadHandle;
#define THREAD_FUNC_RETURN DWORD WINAPI
#define CREATE_THREAD(h, func, arg) \
        h = CreateThread(NULL, 0, func, arg, 0, NULL)
#define JOIN_THREAD(h) WaitForSingleObject(h, INFINITE)
//LINUX
#else
#include <pthread.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/mman.h>
typedef pthread_t ThreadHandle;
#define THREAD_FUNC_RETURN void*
#define CREATE_THREAD(h, func, arg) \
        pthread_create(&h, NULL, func, arg)
#define JOIN_THREAD(h) pthread_join(h, NULL)
#endif

#define LEN_OF_WORD 1024

typedef struct Node {
    char* word;
    char* filename;
    struct Node* next;
} Node;

// struktura pro hash tabulku
typedef struct HashTable {
    size_t size;
    Node** buckets;
#ifdef _WIN32
    HANDLE* mutex_array;
#else
    pthread_mutex_t* mutex_array;
#endif
} HashTable;

//struktura por argumenty vlakna
typedef struct ThreadArg {
    int id;
    char* filename;
    HashTable* table;
} ThreadArg;

//hashovaci funkce
unsigned Hash(char* key, size_t size) {
    unsigned hash = 0;
    for (int i = 0; key[i] != 0; ++i) {
        hash += (unsigned char)(key[i]);//pricteme ASCII hodnotu znaku
    }
    return hash % size;//hash mod velikost tabulky
}

//vytvoreni noveho uzlu
Node* createNode(char* word, char* filename) {
    Node* newNode = (Node*)malloc(sizeof(Node));
    newNode->word = strdup(word);
    newNode->filename = filename; //kopirujeme slovo
    newNode->next = NULL; // inicializace ukazatele na dalsi uzel
    return newNode;
    return newNode;
}

//porovnani dvou uzlu (kontrola duplicity)
bool compare_nodes(Node* node1, Node* node2) {
    return !strcmp(node1->filename, node2->filename) && !strcmp(node1->word, node2->word);
}

//vlozeni uzlu do hashovaci tabulky
void insert_node(Node* node, HashTable* table) {
    unsigned word_hash = Hash(node->word, table->size); //ziskame hash hodnotu
#ifdef _WIN32 
    WaitForSingleObject(table->mutex_array[word_hash], INFINITE); //zamceni mutexu pro bucket
#else
    pthread_mutex_lock(&table->mutex_array[word_hash]);//zamceni mutexu pro bucket
#endif
    Node* first = table->buckets[word_hash];
    if (first == NULL) {
        table->buckets[word_hash] = node;
    }
    else {
        if (compare_nodes(node, first)) {
#ifdef _WIN32
            ReleaseMutex(table->mutex_array[word_hash]);
#else
            pthread_mutex_unlock(&table->mutex_array[word_hash]);
#endif
            return;
        }
        while (first->next) {
            first = first->next;
            if (compare_nodes(node, first)) {
#ifdef _WIN32
                ReleaseMutex(table->mutex_array[word_hash]);
#else
                pthread_mutex_unlock(&table->mutex_array[word_hash]);
#endif
                return;
            }
        }
        first->next = node;
    }
#ifdef _WIN32
    ReleaseMutex(table->mutex_array[word_hash]);
#else
    pthread_mutex_unlock(&table->mutex_array[word_hash]);
#endif
}

// kontrola platnosti slova
bool is_valid_word(char* word) {
    for (int i = 0; word[i] != '\0'; ++i) {
        if (word[i] == '.' || word[i] == ',' || word[i] == '?' || word[i] == '!') {
            return false;
        }
    }
    return true;
}

//cteni slov ze souboru a jejich vkladani do tabulky
void read_words(HashTable* table, char* filename) {
    char word[LEN_OF_WORD];
    int word_index = 0;

#ifdef _WIN32
    //otevre soubor
    HANDLE hFile = CreateFile(filename, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        fprintf(stderr, "Error opening file: %lu\n", GetLastError());
        return;
    }
    // zjisti velikost souboru
    DWORD fileSize = GetFileSize(hFile, NULL);
    if (fileSize == INVALID_FILE_SIZE) {
        fprintf(stderr, "Error getting file size: %lu\n", GetLastError());
        CloseHandle(hFile);
        return;
    }
    // vytvori objekt mapovani souboru
    HANDLE hMapping = CreateFileMapping(hFile, NULL, PAGE_READONLY, 0, 0, NULL);
    if (!hMapping) {
        fprintf(stderr, "Error creating file mapping: %lu\n", GetLastError());
        CloseHandle(hFile);
        return;
    }
    // vytvori mapovani souboru
    char* file_content = (char*)MapViewOfFile(hMapping, FILE_MAP_READ, 0, 0, 0);
    if (!file_content) {
        fprintf(stderr, "Error mapping file: %lu\n", GetLastError());
        CloseHandle(hMapping);
        CloseHandle(hFile);
        return;
    }
#else
    //otevre soubor
    int fd = open(filename, O_RDONLY);
    if (fd == -1) {
        perror("Error opening file");
        return;
    }

    struct stat st;
    if (fstat(fd, &st) == -1) {
        perror("fstat");
        close(fd);
        return;
    }

    size_t file_size = st.st_size;
    char* file_content = mmap(NULL, file_size, PROT_READ, MAP_PRIVATE, fd, 0);
    if (file_content == MAP_FAILED) {
        perror("Error mapping file to memory");
        close(fd);
        return;
    }
#endif
#ifdef _WIN32
    for (DWORD i = 0; i < fileSize; ++i) {
#else
    for (off_t i = 0; i < file_size; ++i) {
#endif
        char c = file_content[i];
        // pokud je znak mezera nebo novy radek, mame slovo
        if (isspace(c)) {
            if (word_index > 0) {
                word[word_index] = '\0'; // ukonceni retezce (slova)
                if (is_valid_word(word)) {
                    Node* node = createNode(word, filename);
                    insert_node(node, table);
                }
                word_index = 0;  // reset pro dalsi slovo
            }
        }
        else {
            //pridat znak do slova
            if (word_index < LEN_OF_WORD - 1) {
                word[word_index++] = c;
            }
        }
    }
#ifdef _WIN32
    UnmapViewOfFile(file_content);
    CloseHandle(hMapping);
    CloseHandle(hFile);
#else
    munmap(file_content, file_size);
    close(fd);
#endif
}

//funkce vlakna
THREAD_FUNC_RETURN thread_func(void* arg) {
    ThreadArg* thread_arg = (ThreadArg*)arg;
    read_words(thread_arg->table, thread_arg->filename);
    return 0;
}

//vytvori hash tabulku pro dvojice <slovo, soubor>
HashTable create_table(size_t size) {
    HashTable table;
    table.size = size;
    table.buckets = (Node**)calloc(size, sizeof(Node*)); //alokace pameti pro bucket
#ifdef _WIN32
    table.mutex_array = (HANDLE*)malloc(size * sizeof(HANDLE));//alokace pameti pro mutexy
    for (size_t i = 0; i < size; ++i) { //inicializace mutexu
        table.mutex_array[i] = CreateMutex(NULL, FALSE, NULL);
    }
#else
    table.mutex_array = (pthread_mutex_t*)calloc(size, sizeof(pthread_mutex_t)); //alokace pameti pro mutexy
    for (size_t i = 0; i < size; ++i) {
        pthread_mutex_init(&table.mutex_array[i], NULL); //inicializace mutexu
    }
#endif
    return table;
}

//vypis bucketu a odstraneni duplicit
Node* write_list(Node* node) {
    printf("%s: %s", node->word, node->filename);
    Node* next_node = node->next;
    Node* new_node = NULL;
    Node* previous_node = node;
    while (next_node) {
        if (!strcmp(next_node->word, node->word)) {
            printf(", %s", next_node->filename);
            Node* tmp = next_node;
            next_node = next_node->next;
            previous_node->next = next_node;
            free(tmp);
        }
        else {
            if (!new_node) {
                new_node = next_node;
            }
            previous_node = next_node;
            next_node = next_node->next;
        }
    }
    printf("\n");
    free(node); //uvolneni aktualniho uzlu
    return new_node;
}

//vypis cele tabulky
void write_table(HashTable* table) {
    for (size_t i = 0; i < table->size; ++i) {
        while (table->buckets[i]) {
            table->buckets[i] = write_list(table->buckets[i]);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 3) { //kontrola poctu argumentu
        printf("Zadejte platny pocet argumentu.\n");
        return 1;
    }

    size_t size = atoi(argv[1]);
    int num_files = argc - 2; //pocet souboru

    ThreadHandle threads[num_files];
    ThreadArg thread_args[num_files];

    HashTable table = create_table(size); //vytvoreni hashovaci tabulky

    for (int i = 0; i < num_files; ++i) {
        thread_args[i].id = i;
        thread_args[i].filename = argv[i + 2];
        thread_args[i].table = &table;
        CREATE_THREAD(threads[i], thread_func, &thread_args[i]);
    }
    // cekani na dokonceni vlaken
    for (int i = 0; i < num_files; ++i) {
        JOIN_THREAD(threads[i]);
    }
 
    write_table(&table);//vypis tabulky
    return 0;
}