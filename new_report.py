class Report:

    def __init__(
            self,
            include_error_data: bool = False,
            max_count_error_data: int = 1000,
    ):
        self.include_error_data = include_error_data
        self.max_count_error_data = max_count_error_data
        self.success_dict = 0
        self.success_data = 0
        self.error_in_dict = 0
        self.error_in_data = 0
        self.error_in_other = 0
        self.summary_report = {}

        if include_error_data:
            self.dict_errors = []
            self.data_errors = []
            self.other_errors = []

    def add_success_dict_message(
            self,
            increment: int = 1,
    ):
        self.success_dict += increment

    def add_success_data_message(
            self,
            increment: int = 1,
    ):
        self.success_data += increment

    def add_error_dict_message(
            self,
            increment: int = 1,
            exception=None,
            data=None,
            index=None,
    ):
        self.error_in_dict += increment
        if self.include_error_data:
            if self.error_in_dict < self.max_count_error_data or self.max_count_error_data == 0:
                error_report = {
                        'exception': exception,
                        'index': index,
                        'data': data,
                    }
                self.dict_errors.append(error_report)

    def add_error_data_message(
            self,
            increment: int = 1,
            exception=None,
            data=None,
            index=None,
    ):
        self.error_in_data += increment
        if self.include_error_data:
            if self.error_in_data < self.max_count_error_data or self.max_count_error_data == 0:
                error_report = {
                        'exception': exception,
                        'index': index,
                        'data': data,
                    }
                self.data_errors.append(error_report)

    def add_error_other_message(
            self,
            increment: int = 1,
            exception=None,
            data=None,
            index=None,
    ):
        self.error_in_other += increment
        if self.include_error_data:
            if self.error_in_other < self.max_count_error_data or self.max_count_error_data == 0:
                error_report = {
                        'exception': exception,
                        'index': index,
                        'data': data,
                    }
                self.other_errors.append(error_report)

    def serialize(
            self,
            location: str = 'both',
    ):
        valid_locations = ['dict', 'data', 'both']
        if location not in valid_locations:
            return f'Invalid location. Choose one {valid_locations}'
        if location == 'dict':
            pass
        if location == 'data':
            pass
        if location == 'both':
            pass
