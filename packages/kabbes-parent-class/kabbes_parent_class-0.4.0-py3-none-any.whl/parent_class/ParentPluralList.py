from parent_class import ParentPlural

class ParentPluralList( ParentPlural ):

    def __init__( self ):

        ParentPlural.__init__( self )

if __name__ == '__main__':
    a = ParentPluralList()
    a.print_atts()