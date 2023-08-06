from parent_class import ParentClass

class ParentPlural( ParentClass ):

    def __init__( self ):

        ParentClass.__init__( self )
   

if __name__ == '__main__':
    a = ParentPlural()
    a.print_atts()