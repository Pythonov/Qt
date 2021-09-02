class ReportInput:

    def __init__(
            self,
            summary_report: dict,
            max_count_error_data: int = 1000,
            locations: list = None,
    ):
        """
        Конструктор класса.
        Передается вид основного (количественного) отчета
        =====summary_report=====
         summary_report = {
        'success_insert': 0,
        'error_insert': 0,
        'error_something_else': 0,
        }
        В случае передачи locations, также будет формироваться
        подробный отчет с указанием мест ошибок и данных о них
        =====locations=====
        locations = ['loc_0', 'loc_1', 'loc_2']
        Максимальное количество ошибок в отчете (на каждую из категорий)
        =====max_count_error_data=====
        """
        self.summary_report = summary_report
        self.max_count_error_data = max_count_error_data
        if locations:
            self.summary_report['error_data'] = {}
            for location in locations:
                self.summary_report['error_data'][f'error_{location}_data'] = []

    def extend_report(
            self,
            target_counter: str,
            increment_size: int = 1,
            location: str = None,
            obj_index: list = None,
            data=None,
            exception=None,
    ):
        self.summary_report[target_counter] += increment_size
        if 'error_data' in self.summary_report and exception:
            if len(self.summary_report['error_data']
                   [f'error_{location}_data']) < self.max_count_error_data or self.max_count_error_data == 0:
                error_report = {
                    'message': str(exception),
                    'data': data,
                    'index': obj_index,
                }
                self.summary_report['error_data'][f'error_{location}_data'].append(error_report)


