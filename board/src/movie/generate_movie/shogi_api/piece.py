#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, copy

class Piece:

    def __init__(self, name, is_sente, loc=None):

        self.name = name
        self.is_sente = is_sente
        self.loc = loc