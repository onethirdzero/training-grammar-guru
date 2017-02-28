#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Copyright 2017 Eddie Antonio Santos <easantos@ualberta.ca>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Tests the generation of sentences.
"""

import pytest

from token_utils import Token
from vectorize_tokens import serialize_tokens
from sentences import forward_sentences, backward_sentences
from vocabulary import vocabulary

FILE = serialize_tokens([
    Token(value='(', type='Punctuator', loc=None),
    Token(value='name', type='Identifier', loc=None),
    Token(value=')', type='Punctuator', loc=None),
    Token(value='=>', type='Punctuator', loc=None),
    Token(value='console', type='Identifier', loc=None),
    Token(value='.', type='Punctuator', loc=None),
    Token(value='log', type='Identifier', loc=None),
    Token(value='(', type='Punctuator', loc=None),
    Token(value='`Hello, ${', type='Template', loc=None),
    Token(value='name', type='Identifier', loc=None),
    Token(value='}!`', type='Template', loc=None),
    Token(value=')', type='Punctuator', loc=None),
    Token(value=';', type='Punctuator', loc=None)
])

assert len(FILE) == 13


def test_forward_sentences():
    """
    Test creatign padded forward sentences.
    """
    n = 10  # sentence length.
    m = n - 1  # context length.

    sentences = list(forward_sentences(FILE, context=m, adjacent=1))

    # Even with padding, there should be the same number of sentences as there
    # are tokens in the original vector.
    assert len(sentences) == len(FILE)

    # Test each sentence generated.
    for i, (context, adjacent) in enumerate(sentences):
        assert len(context) == m
        assert adjacent == FILE[i]

    # The first context should be a context with all padding.
    context, adjacent = sentences[0]
    assert all(index == vocabulary.start_token_index for index in context)

    # Try using ONLY sentence length. Should get the same result.
    assert list(forward_sentences(FILE, sentence=n)) == sentences

    # TODO: test for when sentence size is LARGER than file



def test_backwards_contexts():
    ...


@pytest.mark.skip
def test_both_sentences():
    args = FILE
    kwargs = dict(context=9, result=1)
    combined = zip(forward_sentences(*args, **kwargs),
                   backward_sentences(*args, **kwargs))

    # Check if both contexts are THE SAME.
    i = 1
    for (_, t1), (_, t1) in combined:
        i += 1
        assert t1 == t2
    assert i == len(FILE)