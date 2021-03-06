from ristrettoORM.ristrettoORMUtils import wrap_exception
from ristrettoORMExceptions import DAOMapperException
from ristrettoORM.converters import PropertyConverter

class PropertyMappings(object):

    def __init__(self, propertyName, columnName, converter):
        self.propertyName = propertyName
        self.columnName = columnName
        self.converter = converter

    def getValueFromResultSet(self, resultSet):
        try:
            return self.converter.getValueFromResultSet(self.columnName, resultSet)
        except Exception as e:
            wrap_exception(DAOMapperException, "Failed mapping of values of Result Set because of: {0}".format(e.message))

    def getValue(self, object):
        return self.converter.getValueFromResultSet(self.propertyName, object)

    def setValue(self, object, resultSet):
        """
        def setValue(GroovyObject obj, ResultSet rs) throws Exception {
        propertyValue = this.converter.getValueFromResultSet(columnName, rs)

        setterMethodName = StringUtils.setterMethodName(this.propertyName,obj.class)

        obj.invokeMehod(setterMethodName, propertyValue)
        }
        """
        propertyValue = self.converter.getValueFromResultSet(self.columnName, resultSet)
        setterMethodName = getattr() #TODO: finish this

    def getPropertyType(self):
        return self.converter.getPropertyType()

    def setPropertyType(self, type):
        self.converter = PropertyConverter.getConverterForType(type)

