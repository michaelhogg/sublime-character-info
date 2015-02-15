import sublime, sublime_plugin, unicodedata

# Needed because unicodedata.name() doesn't return names of control characters
# See stackoverflow.com/questions/24552786/why-doesnt-unicodedata-recognise-certain-characters
UNNAMED_CONTROL_CHARS = {
    0x00: 'NULL',
    0x01: 'START OF HEADING',
    0x02: 'START OF TEXT',
    0x03: 'END OF TEXT',
    0x04: 'END OF TRANSMISSION',
    0x05: 'ENQUIRY',
    0x06: 'ACKNOWLEDGE',
    0x07: 'BELL',
    0x08: 'BACKSPACE',
    0x09: 'CHARACTER TABULATION',
    0x0A: 'LF: LINE FEED',
    0x0B: 'LINE TABULATION',
    0x0C: 'FF: FORM FEED',
    0x0D: 'CR: CARRIAGE RETURN',
    0x0E: 'SHIFT OUT',
    0x0F: 'SHIFT IN',
    0x10: 'DATA LINK ESCAPE',
    0x11: 'DEVICE CONTROL ONE',
    0x12: 'DEVICE CONTROL TWO',
    0x13: 'DEVICE CONTROL THREE',
    0x14: 'DEVICE CONTROL FOUR',
    0x15: 'NEGATIVE ACKNOWLEDGE',
    0x16: 'SYNCHRONOUS IDLE',
    0x17: 'END OF TRANSMISSION BLOCK',
    0x18: 'CANCEL',
    0x19: 'END OF MEDIUM',
    0x1A: 'SUBSTITUTE',
    0x1B: 'ESCAPE',
    0x1C: 'INFORMATION SEPARATOR FOUR',
    0x1D: 'INFORMATION SEPARATOR THREE',
    0x1E: 'INFORMATION SEPARATOR TWO',
    0x1F: 'INFORMATION SEPARATOR ONE',
    0x7F: 'DELETE',
    0x80: 'CONTROL U+0080',
    0x81: 'CONTROL U+0081',
    0x82: 'BREAK PERMITTED HERE',
    0x83: 'NO BREAK HERE',
    0x84: 'CONTROL U+0084',
    0x85: 'NEL: NEXT LINE',
    0x86: 'START OF SELECTED AREA',
    0x87: 'END OF SELECTED AREA',
    0x88: 'CHARACTER TABULATION SET',
    0x89: 'CHARACTER TABULATION WITH JUSTIFICATION',
    0x8A: 'LINE TABULATION SET',
    0x8B: 'PARTIAL LINE FORWARD',
    0x8C: 'PARTIAL LINE BACKWARD',
    0x8D: 'REVERSE LINE FEED',
    0x8E: 'SINGLE SHIFT TWO',
    0x8F: 'SINGLE SHIFT THREE',
    0x90: 'DEVICE CONTROL STRING',
    0x91: 'PRIVATE USE ONE',
    0x92: 'PRIVATE USE TWO',
    0x93: 'SET TRANSMIT STATE',
    0x94: 'CANCEL CHARACTER',
    0x95: 'MESSAGE WAITING',
    0x96: 'START OF GUARDED AREA',
    0x97: 'END OF GUARDED AREA',
    0x98: 'START OF STRING',
    0x99: 'CONTROL U+0099',
    0x9A: 'SINGLE CHARACTER INTRODUCER',
    0x9B: 'CONTROL SEQUENCE INTRODUCER',
    0x9C: 'STRING TERMINATOR',
    0x9D: 'OPERATING SYSTEM COMMAND',
    0x9E: 'PRIVACY MESSAGE',
    0x9F: 'APPLICATION PROGRAM COMMAND'
}

def getUnicodeCharName(char):
    charName = unicodedata.name(char, 'Unknown')  # Get the Unicode name assigned to the character
    charCode = ord(char)
    if charName == 'Unknown' and charCode in UNNAMED_CONTROL_CHARS:
        charName = UNNAMED_CONTROL_CHARS[charCode]
    return charName

def updateStatusBar(view):
    char         = view.substr(view.sel()[0].a)  # The character at the cursor or start of selection
    hexCode      = hex(ord(char)).upper().replace('X','x')
    statusString = 'Char ' + hexCode
    viewEncoding = view.encoding()
    if viewEncoding == 'UTF-8' or viewEncoding == 'Undefined':
        # The encoding may be Undefined if the file only contains 7-bit ASCII characters
        # which are common to many encodings (UTF-8, ISO-8859-1, Windows-1251, etc)
        charName = getUnicodeCharName(char)
        statusString += ' (' + charName + ')'
    sublime.status_message(statusString)

class CharacterInfoListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        updateStatusBar(view)
