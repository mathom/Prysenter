#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
sys.path.extend(('.', '..'))

from presentation import Presentation

slides = ['Intro to Prysenter',
          'Prysenter does presentations',
          'Simple',
          'Minimal',
          'Quick',
          'Thank You.',
          'https://github.com/cnelsonsic/Prysenter']
Presentation(slides=slides).start()
