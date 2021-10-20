# This is an automatically generated file. You can find more configuration
# parameters in 'config.py' file.

# The family of sites we are working on. wikipedia.py will import
# families/xxx_family.py so if you want to change this variable,
# you need to write such a file.
family = 'wikipedia'

# The language code of the site we're working on.
mylang = 'nn'

# The dictionary usernames should contain a username for each site where you
# have a bot account. If you have a unique username for all languages of a
# family , you can use '*'
usernames['wikipedia']['nn'] = 'ExampleBot'
usernames['commons']['commons'] = 'ExampleBot'

# The list of BotPasswords is saved in another file. Import it if needed.
# See https://www.mediawiki.org/wiki/Manual:Pywikibot/BotPasswords to know how
# use them.
authenticate['*.wikimedia.org'] = ('supersecretoauth')
authenticate['*.wikipedia.org'] = ('supersecretoauth')
