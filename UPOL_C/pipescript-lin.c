#include <stdio.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <string.h>
#include <sys/stat.h>

#define MAX_LINE_LENGTH 2048 //maximalni delka radku
#define MAX_CMD 1024 // maximalni delka prikazu
#define DELIMITER " " //oddelovac mezi prikazem a argumenty

//fukce pro vytvoreni procesu, ktery spusti prikaz a presmeruje vstup/vystup
int create_process(char* cmd, char* args, int input_fd)
{
    int fds[2]; // pole pro rouru (fds[0] - cteni, fds[1] - zapis)
    pipe(fds); //vytvori rouru
    int pid = fork(); //vytvoreni noveho procesu
    if (pid < 0)
    {
        printf("fork error\n");
        exit(1);
    }
    if (pid == 0) //detsky proces
    {
        if (input_fd >= 0) // pokud existuje vstupni soubor, presmerujeme jeho obsah na stdin
        {
            dup2(input_fd, STDIN_FILENO);
        }
        dup2(fds[1], 1); // presmerovani vystupu na rouru (fds[1)
        char* args2[] = {cmd, args, NULL};

        //spusteni prikazu
        if (execvp(cmd, args2) < 0)
        {
            perror("execvp");
            close(input_fd);
            close(fds[1]);
            _exit(EXIT_FAILURE); // ukonceni detskeho procesu s chybou
        }
        close(fds[1]);
        close(input_fd);
        _exit(EXIT_SUCCESS);
    }
    close(fds[1]);
    waitpid(pid, NULL, 0);
    return fds[0];
}
//fuknce pro ziskani prvniho slova (prikazu) z radku
char* extract_first_word(char* line)
{
    for (int i = 0; i < strlen(line); ++i)
    {
        if (line[i] == ' ') //pokud najdeme mezeru 
        {
            
            char* word = (char*)calloc(i + 1, sizeof(char)); // alokace pameti pro slovo
            strncpy(word, line, i); // kopirovani slova do promenne
            return word;
        }
    }
    //pokud v radku neni mezeera, vracime cely radek
    char* word = calloc(strlen(line) + 1, sizeof(char));
    strcpy(word, line);
    return word;
}

//funkce pro cteni z fd souboru a zapisovani do jineho fd
void read_from_fd(int fd, int out_fd)
{
    char buf[MAX_LINE_LENGTH]; //buffer pro cteni dat
    while (read(fd, buf, MAX_LINE_LENGTH)) //cte data z popisovace
    {
        write(out_fd, buf, strlen(buf)); // zapisuje na vystupni popisovac
    }
}


//funkce pro rozdeleni prikazu a argumentu a spusteni procesu
int split_cmd_args(char* line, int input_fd)
{
    char* cmd = extract_first_word(line);
    if (cmd[0] == '<') // pokud prikaz zacina znakem "<", sjou data nacitana ze souboru
    {
        int fd = create_process("cat", cmd + 1, input_fd); //vytvoreni procesu pro vstupni soubor
        free(cmd);
        return fd;
    }
    else if (cmd[0] == '>') {
        int out_fd = open(cmd + 1, O_WRONLY | O_CREAT | O_TRUNC, 0644); //otevreni souboru pro zapis
        if (out_fd < 0) {
            perror("Unable to open output file");
            exit(1);
        }
        read_from_fd(input_fd, out_fd); //cte data z predchoziho procesu a zapisuje do souboru
        close(out_fd);
        close(input_fd);
        free(cmd);
        return -1;
    }
    //-1, protoze nechci kopirovat mezeru mezi cmd a args
    //ziskani argumentu, ktere nasleduji za prikazem
    int args_len = strlen(line) - strlen(cmd) - 1;
    char* args = NULL;
    if (args_len > 0)
    {
        args = calloc(args_len + 1, sizeof(char));
        //+1, protoze nechci mezeru mezi cmd a args
        strncpy(args, line + strlen(cmd) + 1, args_len);
    }
    int fd = create_process(cmd, args, input_fd); //vytvoreni procesu pro prikaz s argumenty
    free(cmd);
    free(args);
    return fd;
}

//cte prikazy ze souboru a zpracovava je
void read_lines(char* filename)
{
    //otevre soubor v rezimu pro cteni
    FILE* file = fopen(filename, "r");
    if (!file) {
        perror("Chyba při otevírání souboru ");
        return;
    }
    
    char line[MAX_LINE_LENGTH]; //buffer pro radky
    memset(line, 0, MAX_LINE_LENGTH); 
    int fd = -1; //zatim neni prirazeny zadny deskriptor
    int len = 0;
    //kazdy radek ze souboru je nacten do bufferu line o maximalni delce MAX_LINE_LENGTH
    while (fgets(line, MAX_LINE_LENGTH, file))
    {
        // odstraneni noveho radku a navratu na zacatek
        len = strlen(line);
        if (len > 0 && line[len - 1] == '\n') {
            line[len - 1] = '\0';
            --len;
        }    
        if (len > 0 && line[len - 1] == '\r') {
            line[len - 1] = '\0';  
        }
        fd = split_cmd_args(line, fd); //zpracovani prikazu a argumentu
    }
    if (fd > 0)
    {
        read_from_fd(fd, 1);
        close(fd);
    }
    fclose(file);
    return;
}

//funkce pro spusteni procesu s presmerovanim vstupu a vystupu
void execute_with_pipe(char* program, char** args, int input_fd, int output_fd) {
    if (fork() == 0) {
        if (input_fd != -1) {
            dup2(input_fd, STDIN_FILENO); //presmerovani vstupu
            close(input_fd); //zavreni puvodniho popisovace
        }
        if (output_fd != -1) {
            dup2(output_fd, STDOUT_FILENO);//presmerovani vystupu
            close(output_fd); //zavreni puvodniho popisovace
        }
        execvp(program, args); //spusteni prikazu
        perror("execvp");
        exit(EXIT_FAILURE);
    }
}

int main(int argc, char* argv[]) {
    read_lines(argv[1]); //argumentem funkce je soubor, ktery obsahuje prikazy ke zpracovani
    return 0;
}