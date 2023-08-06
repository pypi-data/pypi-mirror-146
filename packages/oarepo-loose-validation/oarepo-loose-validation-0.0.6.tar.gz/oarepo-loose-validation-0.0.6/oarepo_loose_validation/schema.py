from marshmallow import  Schema
import datetime as dt
import uuid
import decimal
import typing


from deepmerge import always_merger
from invenio_records_resources.errors import validation_error_to_list_errors

from marshmallow import base, fields as ma_fields, types
from marshmallow.error_store import ErrorStore
from marshmallow.exceptions import ValidationError
from marshmallow.decorators import (
    POST_DUMP,
    POST_LOAD,
    PRE_DUMP,
    PRE_LOAD,
    VALIDATES,
    VALIDATES_SCHEMA,
)

class ValiditySchema(Schema):
    # def __init__(self):
    #     super().__init__()
    TYPE_MAPPING = {
        str: ma_fields.String,
        bytes: ma_fields.String,
        dt.datetime: ma_fields.DateTime,
        float: ma_fields.Float,
        bool: ma_fields.Boolean,
        tuple: ma_fields.Raw,
        list: ma_fields.Raw,
        set: ma_fields.Raw,
        int: ma_fields.Integer,
        uuid.UUID: ma_fields.UUID,
        dt.time: ma_fields.Time,
        dt.date: ma_fields.Date,
        dt.timedelta: ma_fields.TimeDelta,
        decimal.Decimal: ma_fields.Decimal,
    }  # type: typing.Dict[type, typing.Type[ma_fields.Field]]
    #: Overrides for default schema-level error messages
    error_messages = {}  # type: typing.Dict[str, str]
    def load(
        self,
        data: (
            typing.Mapping[str, typing.Any]
            | typing.Iterable[typing.Mapping[str, typing.Any]]
        ),
        *,
        many: bool | None = None,
        partial: bool | types.StrSequenceOrSet | None = None,
        unknown: str | None = None,
    ):
        """Deserialize a data structure to an object defined by this Schema's fields.

        :param data: The data to deserialize.
        :param many: Whether to deserialize `data` as a collection. If `None`, the
            value for `self.many` is used.
        :param partial: Whether to ignore missing fields and not require
            any fields declared. Propagates down to ``Nested`` fields as well. If
            its value is an iterable, only missing fields listed in that iterable
            will be ignored. Use dot delimiters to specify nested fields.
        :param unknown: Whether to exclude, include, or raise an error for unknown
            fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
            If `None`, the value for `self.unknown` is used.
        :return: Deserialized data

        .. versionadded:: 1.0.0
        .. versionchanged:: 3.0.0b7
            This method returns the deserialized data rather than a ``(data, errors)`` duple.
            A :exc:`ValidationError <marshmallow.exceptions.ValidationError>` is raised
            if invalid data are passed.
        """
        return self._do_load(
            data, many=many, partial=partial, unknown=unknown, postprocess=True
        )

    def _do_load(
            self,
            data: (
                    typing.Mapping[str, typing.Any]
                    | typing.Iterable[typing.Mapping[str, typing.Any]]
            ),
            *,
            many: bool | None = None,
            partial: bool | types.StrSequenceOrSet | None = None,
            unknown: str | None = None,
            postprocess: bool = True,
    ):
        """Deserialize `data`, returning the deserialized result.
        This method is private API.

        :param data: The data to deserialize.
        :param many: Whether to deserialize `data` as a collection. If `None`, the
            value for `self.many` is used.
        :param partial: Whether to validate required fields. If its
            value is an iterable, only fields listed in that iterable will be
            ignored will be allowed missing. If `True`, all fields will be allowed missing.
            If `None`, the value for `self.partial` is used.
        :param unknown: Whether to exclude, include, or raise an error for unknown
            fields in the data. Use `EXCLUDE`, `INCLUDE` or `RAISE`.
            If `None`, the value for `self.unknown` is used.
        :param postprocess: Whether to run post_load methods..
        :return: Deserialized data
        """
        error_store = ErrorStore()
        errors = {}  # type: dict[str, list[str]]
        many = self.many if many is None else bool(many)
        unknown = unknown or self.unknown
        if partial is None:
            partial = self.partial
        # Run preprocessors
        if self._has_processors(PRE_LOAD):
            try:
                processed_data = self._invoke_load_processors(
                    PRE_LOAD, data, many=many, original_data=data, partial=partial
                )
            except ValidationError as err:
                errors = err.normalized_messages()
                result = None  # type: list | dict | None
        else:
            processed_data = data
        if not errors:
            # Deserialize data
            result = self._deserialize(
                processed_data,
                error_store=error_store,
                many=many,
                partial=partial,
                unknown=unknown,
            )
            # Run field-level validation
            self._invoke_field_validators(
                error_store=error_store, data=result, many=many
            )
            # Run schema-level validation
            if self._has_processors(VALIDATES_SCHEMA):
                field_errors = bool(error_store.errors)
                self._invoke_schema_validators(
                    error_store=error_store,
                    pass_many=True,
                    data=result,
                    original_data=data,
                    many=many,
                    partial=partial,
                    field_errors=field_errors,
                )
                self._invoke_schema_validators(
                    error_store=error_store,
                    pass_many=False,
                    data=result,
                    original_data=data,
                    many=many,
                    partial=partial,
                    field_errors=field_errors,
                )
            errors = error_store.errors
            # Run post processors
            if not errors and postprocess and self._has_processors(POST_LOAD):
                try:
                    result = self._invoke_load_processors(
                        POST_LOAD,
                        result,
                        many=many,
                        original_data=data,
                        partial=partial,
                    )
                except ValidationError as err:
                    errors = err.normalized_messages()
        result = processed_data
        if errors:
            exc = ValidationError(errors, data=data, valid_data=result)
            errs = self.handle_error(exc, data, many=many, partial=partial)
            print(errs)
            loosevalidation_errors = []
            invalid_fields = []
            invalid_fields_data = []
            for e in errs:
                for message in e['messages']:
                    if message.__class__.__name__ == 'OarepoError':
                        if not message.struct:
                            error_field = {'path': e['field'], 'key': message, 'structural': False}
                            if message.params:
                                always_merger.merge(error_field, {'params': message.params})
                            loosevalidation_errors.append(error_field)
                        else:
                            error_field = {'path': e['field'], 'key': message, 'structural': True}
                            invalid_value = get_invalid_value(e['field'], result)
                            if invalid_value not in invalid_fields:
                                invalid_fields.append(invalid_value)
                                invalid_field = {'path': e['field'], 'value': invalid_value}
                                invalid_fields_data.append(invalid_field)
                            result = eliminate_invalid_fields(e['field'], result)
                            if message.params:
                                always_merger.merge(error_field, {'params': message.params})

                            loosevalidation_errors.append(error_field)
                    else:
                        error_field = {'path': e['field'], 'key': message, 'structural': True}
                        invalid_value = get_invalid_value(e['field'], result)
                        if invalid_value not in invalid_fields:
                            invalid_fields.append(invalid_value)
                            invalid_field = {'path': e['field'], 'value': invalid_value}
                            invalid_fields_data.append(invalid_field)
                        result = eliminate_invalid_fields(e['field'], result)

                        loosevalidation_errors.append(error_field)

            always_merger.merge(result, {'validace': {'invalid_fields': invalid_fields_data}})
            always_merger.merge(result, {'validace': {'errors': loosevalidation_errors}})

        return result

    def handle_error(
        self, error: ValidationError, data: typing.Any, *, many: bool, **kwargs
    ):
        """Custom error handler function for the schema.

        :param error: The `ValidationError` raised during (de)serialization.
        :param data: The original input data.
        :param many: Value of ``many`` on dump or load.
        :param partial: Value of ``partial`` on load.

        .. versionadded:: 2.0.0

        .. versionchanged:: 3.0.0rc9
            Receives `many` and `partial` (on deserialization) as keyword arguments.
        """
        return validation_error_to_list_errors(error)


def get_invalid_value(path, result):

    data = result
    path_array = path.split('.')
    for x in path_array:
        try:
            data = data[x]
        except:
            data = None
            break
    return data

def eliminate_invalid_fields(path, result):

    path_array = path.split('.')
    last_part = path_array[-1]
    path_array = path_array[:-1]
    print(last_part)
    print(path_array)
    i = 0
    data = result
    for path_part in path_array:
        if path_part in data:
            data = data[path_part]
            i = i + 1
        else:
            break
        if(i == len(path_array) and last_part in data):
            data.pop(last_part)
            break
    return result
