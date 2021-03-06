#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import os
import time
import sys

SHAMELESS_ADVERTISING = "Prysenter\nhttp://git.io/prysenter"

def typewriter(duration_between_key):
    def transition(text):
        for c in text:
            sys.stdout.write(c)
            sys.stdout.flush()
            if not c.isspace():
                time.sleep(duration_between_key)
        sys.stdout.write('\n')
    return transition

def typewriter(duration_between_key):
    def transition(text):
        for c in text:
            sys.stdout.write(c)
            sys.stdout.write('\a')
            sys.stdout.flush()
            if not c.isspace():
                time.sleep(duration_between_key)
        sys.stdout.write('\n')
    return transition

def slider(cols, delay):
    delay_step = float(delay) / cols
    def transition(text):
        for line in text.split('\n'):

            # don't waste time animating invisible stuff
            if not line or line.isspace():
                sys.stdout.write(line)
                sys.stdout.write('\n')
                continue

            width = len(line)
            for offset in range(width, 0, -1):
                sys.stdout.write(' '*offset)
                sys.stdout.write(line[0:width-offset-1])
                sys.stdout.flush()
                if offset:
                    sys.stdout.write('\r'*width)
                time.sleep(delay_step)

            sys.stdout.write('\a')
            sys.stdout.write('\n')
    return transition


def springy(cols, delay):
    delay_step = float(delay) / cols
    def transition(text):
        for line in text.split('\n'):

            # don't waste time animating invisible stuff
            if not line or line.isspace():
                sys.stdout.write(line)
                sys.stdout.write('\n')
                continue

            width = len(line)
            x = width / 2
            v = 1
            k = 0.25
            m = 0.8
            d = 0.75
            dt = delay_step
            while abs(v) > 0.03:
                f = -k * x
                a = f / m
                v = d * (v + a)
                x += v
                sys.stdout.write('\r'*width)
                xi = int(x)
                sys.stdout.write(('\r' if x<0 else ' ')*abs(xi))
                sys.stdout.write(line[-(x<0)*xi:width-xi])
                sys.stdout.flush()
                time.sleep(dt)

            sys.stdout.write('\a')
            sys.stdout.write('\n')
    return transition


def no_transition(text):
    print text

class Presentation(object):
    '''Show a text-based presentation in your terminal.
    Make sure your font size is cranked to 72 or something
    equally ridiculous.
    Fair warning: Long, verbose slides are NOT SUPPORTED.
    Remember: smaller, quicker hunks of info to remind
    people what you are talking about.
    '''
    def __init__(self, slides):
        '''Initialize our presentation.
        Takes a list of slide strings like:
        >>> Presentation(['Why prysenter is cool.', 'It lets you do tiny slides.'])
        '''
        self.slides = list(slides)
        self.current_slide = self.slides[0]

    def __del__(self):
        # Turning the cursor on here so we get our cursor back
        # even on errors.
        self.cursor()

    def cursor(self, state='on'):
        '''State should be 'on' or 'off'.'''
        os.system('setterm -cursor %s' % state)

    @staticmethod
    def get_term_size():
        '''Gets the size of your terminal. May not work everywhere. YMMV.'''
        rows, columns = os.popen('stty size', 'r').read().split()
        return int(rows), int(columns)

    @staticmethod
    def strip_ws(string):
        '''Strip leading whitespace around multiline strings.'''
        return '\n'.join((line.strip() for line in string.split("\n")))

    @staticmethod
    def center(string, width):
        '''Center all lines of a string horizontally.'''
        return '\n'.join((line.center(width) for line in string.split("\n")))

    @staticmethod
    def clear():
        '''Clears the screen. Should work everywhere.'''
        os.system('cls' if os.name=='nt' else 'clear')

    @staticmethod
    def wait():
        '''Wait for the presenter to hit "Enter", then return.'''
        # TODO: Could be a fancy input loop and wait for any input at all?
        raw_input()

    def do_slide(self, slide=None):
        '''Print the given slide to the terminal.'''
        # We weren't passed a specific slide, just show the current one.
        if not slide:
            transition = no_transition
            if len(self.current_slide) == 2:
                slide, transition = self.current_slide
            else:
                slide = self.current_slide

        rows, cols = self.get_term_size()

        # How many rows tall is the slide?
        slide_height = len(slide.split("\n"))

        # Determine our top margin,
        # subtracting the slide height if it's more than one line
        top_margin = (rows-(slide_height if slide_height > 1 else 0))/2

        # Print newlines to bump the slide text downward enough
        # Remember that print adds a new line, hence -1.
        print "\n"*(top_margin-1)

        # Strip whitespace and center it horizontally.
        slide = self.center(self.strip_ws(slide), cols)
        transition(slide)

    def start(self):
        '''Start the presentation.
        This will loop as long as there are slides left.'''

        # Tack on our advertising slide:
        self.slides.append(SHAMELESS_ADVERTISING)

        # This is a while instead of a for in case we implement slides that can
        # point to other slides. ¯\°_o/¯
        self.cursor(state='off')
        while self.slides:
            self.clear()
            self.do_slide()
            self.wait()

            try:
                # Next slide!
                s = self.slides # Shorthand for later.
                self.current_slide = s[s.index(self.current_slide)+1]
            except IndexError:
                # Out of slides!
                # Clear the screen before we end the presentation so junk isnt left over.
                self.clear()
                break
        self.cursor()

if __name__ == "__main__":
    slide3 = '''So as I was saying,
    there are lots of things that I would like to talk about.
    One of which is stuff.
    This slide is plain lucky.'''

    slide4 = '''Oh god what are you doing.
    Why is this slide so long?!
    What is wrong with you?!!?
    Just put it on different slides.
    Why don't you just fire up vim.
    You obviously have a lot to say.
    You should read the documentation.
    You know they're already bored.'''

    p = Presentation(["asfasdf", "werqwerqewrqwerqwer", slide3, slide4])
    p.start()
