from celery import shared_task
from .views import ExportActivities, ExportTransactions, ExportTransactionSectors, ExportTransactionLocations, ExportTransactionSectorLocations, ExportBudgetLocations, ExportBudgets, ExportBudgetSectors, ExportBudgetSectorLocations


@shared_task
def cache_workbooks():
    models = (ExportActivities, ExportTransactions, ExportTransactionSectors, ExportTransactionLocations, ExportTransactionSectorLocations, ExportBudgetLocations, ExportBudgets, ExportBudgetSectors, ExportBudgetSectorLocations)
    formats = ('xlsx', 'csv', 'csv_raw')
    for model in models:
        for export_format in formats:
            instance = model(always_refresh_cache=True, export_format=export_format)
            instance.generate_response()
