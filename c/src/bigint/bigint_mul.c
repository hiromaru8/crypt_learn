
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
 * 多倍長整数同士の乗算を行う。
 *
 * left  : 被乗数（num_words ワード）
 * right : 乗数   （num_words ワード）
 * result: 乗算結果格納先（2 * num_words ワード）
 *
 * 筆算方式（Long Multiplication）により、
 *
 *     result = left × right
 *
 * を計算する。
 *
 * 結果の各ワードを下位ワードから順に求めながら、
 * キャリーを r0, r1, r2 の3ワードで管理する。
 *
 *     r2 | r1 | r0
 *
 * r0 : 現在計算中の結果ワード
 * r1 : 次ワードへのキャリー
 * r2 : r1 からさらにあふれたキャリー
 *
 * result 配列は 2 * num_words ワード以上の領域を
 * 確保しておく必要がある。
 */
static void uECC_vli_mult(uECC_word_t *result,
                          const uECC_word_t *left,
                          const uECC_word_t *right,
                          wordcount_t num_words)
{
    /* 部分和およびキャリーを保持する3ワードの累算器 */
    uECC_word_t r0 = 0; /* 現在の出力ワード */
    uECC_word_t r1 = 0; /* 次ワードへのキャリー */
    uECC_word_t r2 = 0; /* r1 を超えるキャリー */

    wordcount_t i, k;

    /*
     * 乗算結果の下位半分を計算する。
     *
     * result[k] =
     *      left[0] * right[k]
     *    + left[1] * right[k-1]
     *    + ...
     *    + left[k] * right[0]
     *
     * これは乗算行列の左下三角部分に対応する。
     */
    for (k = 0; k < num_words; ++k) {

        for (i = 0; i <= k; ++i) {
            muladd(left[i],
                   right[k - i],
                   &r0, &r1, &r2);
        }

        /* 計算が完了した結果ワードを格納 */
        result[k] = r0;

        /* 次の桁の計算に向けてキャリーを繰り上げる */
        r0 = r1;
        r1 = r2;
        r2 = 0;
    }

    /*
     * 乗算結果の上位半分を計算する。
     *
     * result[k] =
     *      left[k+1-num_words] * right[num_words-1]
     *    + ...
     *    + left[num_words-1] * right[k-(num_words-1)]
     *
     * これは乗算行列の右上三角部分に対応する。
     */
    for (k = num_words; k < num_words * 2 - 1; ++k) {

        for (i = (k + 1) - num_words;
             i < num_words;
             ++i) {

            muladd(left[i],
                   right[k - i],
                   &r0, &r1, &r2);
        }

        /* 計算が完了した結果ワードを格納 */
        result[k] = r0;

        /* 次の桁の計算に向けてキャリーを繰り上げる */
        r0 = r1;
        r1 = r2;
        r2 = 0;
    }

    /* 最上位ワードを格納 */
    result[num_words * 2 - 1] = r0;
}