// This file is part of TestCov,
// a robust test executor with reliable coverage measurement:
// https://gitlab.com/sosy-lab/software/test-suite-validator/
//
// Copyright (C) 2018 - 2020  Dirk Beyer
// SPDX-FileCopyrightText: 2019 Dirk Beyer <https://www.sosy-lab.org>
//
// SPDX-License-Identifier: Apache-2.0

#define MAX_INPUT_SIZE 3000
#ifdef GCOV
extern void __gcov_dump(void);
#endif

void abort_prog() {
#ifdef GCOV
  __gcov_dump();
#endif
  abort();
}

void __VERIFIER_assume(int cond) {
  if (!cond) {
    abort_prog();
  }
}

char *get_input();

// taken from https://stackoverflow.com/a/32496721
void replace_char(char *str, char find, char replace) {
  char *current_pos = strchr(str, find);
  while (current_pos) {
    *current_pos = replace;
    current_pos = strchr(current_pos, find);
  }
}

void parse_input_from(char *inp_var, char *format, void *destination) {
  char format_with_fallback[13];
  strcpy(format_with_fallback, format);
  strcat(format_with_fallback, "%c%c%c%c");
  if (inp_var[0] == '0' && inp_var[1] == 'x') {
    replace_char(format_with_fallback, 'd', 'x');
    replace_char(format_with_fallback, 'u', 'x');
  } else {
    if (inp_var[0] == '\'' || inp_var[0] == '\"') {
      int inp_length = strlen(inp_var);
      // Remove ' at the end
      inp_var[inp_length - 1] = '\0';
      // Remove ' in the beginning
      inp_var++;
    }
  }
  char leftover[4];
  int filled = sscanf(inp_var, format_with_fallback, destination, &leftover[0],
                      &leftover[1], &leftover[2], &leftover[3]);
  _Bool is_valid = 1;
  if (filled == 5 || filled == 0) {
    is_valid = 0;
  }
  while (filled > 1) {
    filled--;
    char literal = leftover[filled - 1];
    switch (literal) {
    case 'l':
    case 'L':
    case 'u':
    case 'U':
    case 'f':
    case 'F':
      break;
    default:
      is_valid = 0;
    }
  }

  if (!is_valid) {
    fprintf(stderr, "Can't parse input: '%s'\n", inp_var);
    abort_prog();
  }
}

void parse_input(char *format, void *destination) {
  char *inp_var = get_input();
  parse_input_from(inp_var, format, destination);
}

char __VERIFIER_nondet_char() {
  char val;
  char *inp_var = get_input();
  if (inp_var[0] == '\'') {
    parse_input_from(inp_var, "%c", &val);
  } else {
    parse_input_from(inp_var, "%hhd", &val);
  }
  return val;
}

unsigned char __VERIFIER_nondet_uchar() {
  unsigned char val;
  parse_input("%hhu", &val);
  return val;
}

short __VERIFIER_nondet_short() {
  short val;
  parse_input("%hd", &val);
  return val;
}

unsigned short __VERIFIER_nondet_ushort() {
  unsigned short val;
  parse_input("%hu", &val);
  return val;
}

int __VERIFIER_nondet_int() {
  int val;
  parse_input("%d", &val);
  return val;
}

unsigned int __VERIFIER_nondet_uint() {
  unsigned int val;
  parse_input("%u", &val);
  return val;
}

long __VERIFIER_nondet_long() {
  long val;
  parse_input("%ld", &val);
  return val;
}

unsigned long __VERIFIER_nondet_ulong() {
  unsigned long val;
  parse_input("%lu", &val);
  return val;
}

long long __VERIFIER_nondet_longlong() {
  long long val;
  parse_input("%lld", &val);
  return val;
}

unsigned long long __VERIFIER_nondet_ulonglong() {
  unsigned long long val;
  parse_input("%llu", &val);
  return val;
}

float __VERIFIER_nondet_float() {
  float val;
  parse_input("%f", &val);
  return val;
}

double __VERIFIER_nondet_double() {
  double val;
  parse_input("%lf", &val);
  return val;
}

_Bool __VERIFIER_nondet_bool() { return (_Bool)__VERIFIER_nondet_int(); }

void *__VERIFIER_nondet_pointer() { return (void *)__VERIFIER_nondet_ulong(); }

unsigned int __VERIFIER_nondet_size_t() { return __VERIFIER_nondet_uint(); }

unsigned char __VERIFIER_nondet_u8() { return __VERIFIER_nondet_uchar(); }

unsigned short __VERIFIER_nondet_u16() { return __VERIFIER_nondet_ushort(); }

unsigned int __VERIFIER_nondet_u32() { return __VERIFIER_nondet_uint(); }

unsigned int __VERIFIER_nondet_U32() { return __VERIFIER_nondet_u32(); }

unsigned char __VERIFIER_nondet_unsigned_char() {
  return __VERIFIER_nondet_uchar();
}

unsigned int __VERIFIER_nondet_unsigned() { return __VERIFIER_nondet_uint(); }

const char *__VERIFIER_nondet_string() {
  char *val = malloc(MAX_INPUT_SIZE + 1);
  // Read to end of line
  parse_input("%[^\n]", val);
  return val;
}
