#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <signal.h>

#define NUM_OF_ARGUMENTS 3

size_t blocks_transferred = 0; // pocet prenesenych bloku
size_t bytes_transferred = 0;  // pocet prenesenych bajtu
size_t total_size = 0;                  // celkova velikost dat
//obsluzna funkce  pro signal SIGQUIT
void my_printf(int id){
    fprintf(stderr, "\nPøeneseno blokù: %zu\n", blocks_transferred);
    double percentage = (total_size == 0) ? 0.0 : (100.0 * bytes_transferred / total_size);
    fprintf(stderr, "Procento pøenesených dat: %.2f%%\n", percentage);
}

// otevre existujici soubor
int open_file(const char* filename, int flags, mode_t mode) {
    int fd = open(filename, flags, mode);
    if (fd == -1) {
        perror("open");
        return 1;
    }
    return fd;
}

// uzavre soubor
void close_file(int fd) {
    if (close(fd) == -1) {
        perror("close");
    }
}

// provede mapovani souboru do pameti
char* create_mmap(int fd, size_t size, int prot, int flags, off_t offset) {
   char* data = mmap(NULL, size, prot, flags, fd, offset);
    if (data == MAP_FAILED) {
        perror("mmap");
        return NULL;
    }
    return data;
}

// uzavre mapovani
void close_mmap(void* data, size_t length) {
    if (munmap(data, length) == -1) {
        perror("munmap");
    }
}

int main(int argc, char* argv[]) {
    struct sigaction sa;
    sa.sa_handler = my_printf;
    sa.sa_flags = 0;
    sigemptyset(&sa.sa_mask);

    if (sigaction(SIGINT, &sa, NULL) == -1) {
        perror("sigaction");
        return 1;
    }
    // kontrola poctu argumentu
    if (argc != NUM_OF_ARGUMENTS + 1) {
        fprintf(stderr, "pouzijte 3 argumenty ve formatu if=<vstupni_soubor> of=<vystupni_soubor> bs=<velikost_bloku>.\n");
        return 1;
    }
    char* input_file = NULL;
    char* output_file = NULL;
    size_t block_size = 0;
    // zpracovani argumentu
    for (int i = 1; i <= NUM_OF_ARGUMENTS; i++) {
        if (strncmp(argv[i], "if=", 3) == 0) { //vstupni soubor
            input_file = argv[i] + 3;
        }
        else if (strncmp(argv[i], "of=", 3) == 0) { //vystupni soubor
            output_file = argv[i] + 3;
        }
        else if (strncmp(argv[i], "bs=", 3) == 0) { //velikost bloku
            block_size = (size_t)atoi(argv[i] + 3);
            if (block_size == 0) {
                fprintf(stderr, "Neplatná velikost bloku.\n");
                return 1;
            }
        }
        else {
            fprintf(stderr, "Neznámý argument: %s\n", argv[i]);
            return 1;
        }
    }

    //otevreni vstupniho souboru
    int input_fd = open_file(input_file, O_RDONLY, 0);
    
    // ziskani veliksti vstupniho souboru
    struct stat st;
    if (fstat(input_fd, &st) == -1) {
        perror("fstat");
        close_file(input_fd);
        return 1;
    }
    size_t file_size = st.st_size;

    //otevreni vystupniho souboru
    int output_fd = open_file(output_file, O_CREAT | O_RDWR, S_IRUSR | S_IWUSR);
    if (output_fd == -1) {
        close_file(input_fd);
        return 1;
    }
    //nastaveni velikosti vystupniho souboru na velikost vstupniho
    if (ftruncate(output_fd, file_size) == -1) {
        perror("ftruncate");
        close_file(input_fd);
        close_file(output_fd);
        return 1;
    }

    //mapovani vstupniho souboru do pameti
    void* input_data = create_mmap(input_fd, file_size, PROT_READ, MAP_PRIVATE, 0);
    if (!input_data) {
        close_file(input_fd);
        close_file(output_fd);
        return 1;
    }

    //mapovani vystupniho souboru do pameti
    void* output_data = create_mmap(output_fd, file_size, PROT_WRITE, MAP_SHARED, 0);
    if (!output_data) {
        close_mmap(input_data, file_size);
        close_file(input_fd);
        close_file(output_fd);
        return 1;
    }
    //kopirovani dat po blocich
    size_t offset = 0;
    while (offset < file_size) {
        size_t copy_size = (offset + block_size > file_size) ? (file_size - offset) : block_size;
        memcpy(output_data + offset, input_data + offset, copy_size);
        offset += copy_size;

        // aktualizace pocitadel
        blocks_transferred++;
        bytes_transferred += copy_size;
        printf("%li\n", copy_size);
    }

    close_mmap(input_data, file_size);
    close_mmap(output_data, file_size);
    close_file(input_fd);
    close_file(output_fd);

    printf("Kopirovani dokonceno.\n");
    return 0;
}