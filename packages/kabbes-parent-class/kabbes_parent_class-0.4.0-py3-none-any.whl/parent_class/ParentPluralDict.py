from parent_class import ParentPlural

class ParentPluralDict( ParentPlural ):

    def __init__( self ):

        ParentPlural.__init__( self )

if __name__ == '__main__':
    a = ParentPluralDict()
    a.print_atts()