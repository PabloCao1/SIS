function initDataTable(selector) {
    //Confguracion general de dt
    var dataTable = new DataTable(selector, {
        layout: {
            top: 'search',
            topStart: 'pageLength',
            topEnd: 'buttons',
            bottomStart: 'info',
            bottomEnd: 'paging'
        },
        responsive: true,
        language: { url: 'https://cdn.datatables.net/plug-ins/2.0.1/i18n/es-ES.json' },
        buttons: [
            'copy',
            'pdf',
            'print'
        ],
        pagingType: 'simple_numbers'
    });

    // Agregar funcionalidad al hacer clic en las filas
    $(selector + ' tbody').on('click', 'tr', function () {
        var data = dataTable.row(this).data();
        var href = $(this).data("href");
        if (data !== undefined && href !== undefined) {
            window.location = href;
        }
    });

    return dataTable;
}

