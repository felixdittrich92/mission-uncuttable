from six import with_metaclass

def classmaker(ClassA, ClassB):
    class Meta(type(ClassA), type(ClassB)):
        pass
    return with_metaclass(Meta, ClassA, ClassB)