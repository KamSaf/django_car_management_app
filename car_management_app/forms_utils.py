
class FormUtils:

    data_errors = {}

    # checks if string field value is proper length, return True if field is proper length
    @staticmethod
    def check_field_length(value: str, length: int) -> bool:
        return False if len(value) > length else True

    # clears displayed error messages list
    def clear_errors(self):
        self.data_errors = {}
        return self

    # set field_too_long error to a form field
    def set_length_errors(self, field_name: str):
        error = f"{field_name} {self.error_messages['field_too_long']}"
        self.data_errors[f'id_{field_name.lower()}'] = error
        self._errors[field_name.lower()] = self.error_class([error])
