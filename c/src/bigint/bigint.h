/*

* This file contains code derived from TinyCrypt Cryptographic Library
* and micro-ecc.
*
* Original copyright:
* Copyright (c) 2017 Intel Corporation
* Copyright (c) 2014 Kenneth MacKay
*
* Modifications:
* Copyright (c) 2026 <Your Company Name>
*
* The original software is distributed under BSD-style licenses.
* See LICENSE_THIRD_PARTY.txt for the complete license texts.
*
* Changes from the original source may have been made to support
* project-specific requirements, portability, optimization, or maintenance.
  */


#include <stdint.h>

/* defining data types to store word and bit counts: */
typedef int8_t wordcount_t;
typedef int16_t bitcount_t;

/* defining data type to store ECC coordinate/point in 32bits words: */
typedef unsigned int uECC_word_t;

/* defining data type to store an ECC coordinate/point in 64bits words: */
typedef uint64_t uECC_dword_t;
