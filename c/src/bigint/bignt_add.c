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


#include "bigint.h"

/*
 * cond が真(1)なら p_true を返し、
 * 偽(0)なら p_false を返す。
 *
 * if文を使わずに実装することで、
 * 実行時間を条件によって変化させない
 * （タイミング攻撃対策）。
 */
uECC_word_t cond_set(uECC_word_t p_true,
                     uECC_word_t p_false,
                     unsigned int cond)
{
    return (p_true * cond) | (p_false * (!cond));
}

/*
 * 多倍長整数加算
 *
 * result = left + right
 *
 * 各配列要素は 1ワード(32bit または 64bit)で、
 * 配列の下位ワードから順に加算する。
 *
 * 戻り値:
 *   最上位ワードからのキャリー
 *   (0 または 1)
 */
static uECC_word_t uECC_vli_add(uECC_word_t *result,
                                const uECC_word_t *left,
                                const uECC_word_t *right,
                                wordcount_t num_words)
{
    /* 前ワードからのキャリー */
    uECC_word_t carry = 0;

    wordcount_t i;

    for (i = 0; i < num_words; ++i) {

        /*
         * 現在ワードの加算
         *
         * sum = left[i] + right[i] + carry
         */
        uECC_word_t sum = left[i] + right[i] + carry;

        /*
         * オーバーフロー判定
         *
         * unsigned加算ではオーバーフローすると
         * 結果が元の被加数より小さくなる。
         *
         * val = 1 : left[i] + right[i] の時点で
         *           オーバーフロー発生
         * val = 0 : オーバーフローなし
         */
        uECC_word_t val = (sum < left[i]);

        /*
         * 次ワードへ渡すキャリーを計算
         *
         * sum != left[i]
         *   → right[i] + carry が 0 ではない
         *     この場合は val がそのままキャリー
         *
         * sum == left[i]
         *   → right[i] + carry == 0
         *     (right[i] = MAX, carry = 1 の場合など)
         *     val だけでは判定できないため、
         *     前の carry を保持する
         *
         * 分岐を使わず cond_set() で選択する。
         */
        carry = cond_set(val, carry, (sum != left[i]));

        /* 結果格納 */
        result[i] = sum;
    }

    /* 最上位ワードからのキャリー */
    return carry;
}
