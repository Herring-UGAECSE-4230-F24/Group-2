OBJS = 0_AddressMap.o

ifdef DEBUG
DEBUGFLGS = -g

else
DEBUGFLGS =
endif

%.o : %.s
	as $(DEBUGFLGS) $< -o $@
0_AddressMap: $(OBJS)
	ld -o 0_AddressMap $(OBJS)

clean: $(OBJS)
	rm *.o 0_AddressMap
