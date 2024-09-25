#Program name
PROG = 1_flags_ex5_13
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
