#Program name
PROG = 4_lower_prog5_2
OBJS = ${PROG}.o

DEBUG = 1

ifdef DEBUG
DEBUGFLGS = -g

else
DEBUGFLGS = 
endif

%.o : %.s
	as $(DEBUGFLGS) $< -o $@
${PROG}: $(OBJS)
	ld -o ${PROG} $(OBJS)

clean: $(OBJS)
	rm *.o ${PROG}