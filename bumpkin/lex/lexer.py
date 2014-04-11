from rply import LexerGenerator


lg = LexerGenerator()

lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
# lg.add('LBRACKET', r'\[')
# lg.add('RBRACKET', r'\]')

lg.add('IDENTIFIER', r'[^()\[\]{}\s#]+')

lg.ignore(r'#.*(?=\r|\n|$)')
lg.ignore(r'\s+')

lexer = lg.build()
