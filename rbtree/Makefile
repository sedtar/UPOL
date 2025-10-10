CFLAGS = -pg -g # Pøepínaèe pro profilování a ladìní

main: main.o rbtree.o
	gcc $(CFLAGS) -o main main.o rbtree.o

main.o: main.c rbtree.h
	gcc $(CFLAGS) -c main.c 

rbtree.o: rbtree.c rbtree.h
	gcc $(CFLAGS) -c rbtree.c 

clean:
	rm -f rbtree
	rm -f *.o