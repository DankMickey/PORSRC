import random

class ChatGarbler:

    def getMessages(self):
        return ['']

    def garble(self, numWords):
        wordList = self.getMessages()
        return '\x01italic\x01%s\x02' % ' '.join([random.choice(wordList) for i in xrange(numWords)])
