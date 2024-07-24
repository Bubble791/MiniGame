include config.mk

TOOLCHAIN := $(DEVKITARM)
MODERN := 1
# don't use dkP's base_tools anymore
# because the redefinition of $(CC) conflicts
# with when we want to use $(CC) to preprocess files
# thus, manually create the variables for the bin
# files, or use arm-none-eabi binaries on the system
# if dkP is not installed on this system

ifneq (,$(TOOLCHAIN))
ifneq ($(wildcard $(TOOLCHAIN)/bin),)
export PATH := $(TOOLCHAIN)/bin:$(PATH)
endif
endif

PREFIX := arm-none-eabi-
OBJCOPY := $(PREFIX)objcopy
OBJDUMP := $(PREFIX)objdump
AS := $(PREFIX)as
CC := $(PREFIX)gcc
LD := $(PREFIX)ld
CPP := $(PREFIX)cpp
NM := $(PREFIX)nm

C_SUBDIR = src
C_BUILDDIR = build/$(C_SUBDIR)
ASM_SUBDIR = asm
ASM_BUILDDIR = build/$(ASM_SUBDIR)
OBJ_DIR := build

SHELL := /bin/bash -o pipefail

MAKEFLAGS += --no-print-directory

ifeq ($(OS),Windows_NT)
EXE := .exe
else
EXE :=
endif

PREPROC := tools/preproc/preproc$(EXE)
ARMIPS := tools/armips.exe
GFX := tools/gbagfx/gbagfx$(EXE)
SCANINC := tools/scaninc/scaninc$(EXE)

CFLAGS := -mthumb -mno-thumb-interwork -mcpu=arm7tdmi -mtune=arm7tdmi -mno-long-calls -march=armv4t -O2 -fira-loop-pressure -fipa-pta
ASFLAGS := -mthumb
CPPFLAGS := -iquote include -Wno-trigraphs -DMODERN=$(MODERN)
LDFLAGS := BPRE.ld -T linker.ld

MODERNCC := $(PREFIX)gcc
PATH_MODERNCC := PATH="$(PATH)" $(MODERNCC)
CC1              = $(shell $(PATH_MODERNCC) --print-prog-name=cc1) -quiet

C_SRCS_IN := $(wildcard $(C_SUBDIR)/*.c $(C_SUBDIR)/*/*.c $(C_SUBDIR)/*/*/*.c)
C_SRCS := $(foreach src,$(C_SRCS_IN),$(if $(findstring .inc.c,$(src)),,$(src)))
C_OBJS := $(patsubst $(C_SUBDIR)/%.c,$(C_BUILDDIR)/%.o,$(C_SRCS))

ASM_SRCS := $(wildcard $(ASM_SUBDIR)/*.s)
ASM_OBJS := $(patsubst $(ASM_SUBDIR)/%.s,$(ASM_BUILDDIR)/%.o,$(ASM_SRCS))

OBJS     := $(C_OBJS) $(ASM_OBJS)

SUBDIRS  := $(sort $(dir $(OBJS)))
$(shell mkdir -p $(SUBDIRS))

# Delete files that weren't built properly
.DELETE_ON_ERROR:

.PHONY: all

all: build/output.bin test.sym
	@./scripts/insert.py --offset $(OFFSET) --output $(OUTPUT_NAME) --input $(ROM_NAME)

%.s: ;
%.png: ;
%.pal: ;
%.aif: ;

%.1bpp: %.png  ; $(GFX) $< $@
%.4bpp: %.png  ; $(GFX) $< $@
%.8bpp: %.png  ; $(GFX) $< $@
%.gbapal: %.pal ; $(GFX) $< $@
%.gbapal: %.png ; $(GFX) $< $@
%.lz: % ; $(GFX) $< $@
%.rl: % ; $(GFX) $< $@

define C_DEP
$1: $2 $$(shell $(SCANINC) -I include -I tools/agbcc/include $2)
endef
$(foreach src, $(C_SRCS), $(eval $(call C_DEP,$(patsubst $(C_SUBDIR)/%.c,$(C_BUILDDIR)/%.o,$(src)),$(src),$(patsubst $(C_SUBDIR)/%.c,%,$(src)))))

build/output.bin: $(OBJS)
	$(LD) $(LDFLAGS) -o build/linker.o $(OBJS)
	@$(OBJCOPY) -O binary build/linker.o build/output.bin
	@$(OBJDUMP) -t build/linker.o > build/rom.sym
	@$(NM) build/linker.o > build/rom_1.sym

$(C_BUILDDIR)/%.o: $(C_SUBDIR)/%.c
	$(CPP) $(CPPFLAGS) $< | $(PREPROC) $< charmap.txt -i | $(CC1) $(CFLAGS) -o - - | cat - <(echo -e ".text\n\t.align\t2, 0") | $(AS) $(ASFLAGS) -o $@ -

$(ASM_BUILDDIR)/%.o: $(ASM_SUBDIR)/%.s
	$(AS) $(ASFLAGS) -o $@ -c $<

clean:
	find . \( -iname '*.1bpp' -o -iname '*.4bpp' -o -iname '*.8bpp' -o -iname '*.gbapal' -o -iname '*.lz' -o -iname '*.rl' -o -iname '*.latfont' -o -iname '*.hwjpnfont' -o -iname '*.fwjpnfont' \) -exec rm {} +
	rm -rf build

test.sym: build/linker.o
	$(OBJDUMP) -t $< > $@