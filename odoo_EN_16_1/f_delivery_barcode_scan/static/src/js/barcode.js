odoo.define('f_delivery_barcode_scan.barcode_handler', function (require) {
    "use strict";

    const fieldRegistry = require('web.field_registry');
    const AbstractField = require('web.AbstractField');
    const core = require('web.core');
    const rpc = require('web.rpc');

    const _t = core._t;

    const BarcodeField = AbstractField.extend({
        supportedFieldTypes: ['char'],
        events: {
            'change': '_onInputChange',
        },

        _onInputChange: function (ev) {
            const barcode = ev.target.value.trim();
            if (barcode) {
                this._scanBarcode(barcode);
                ev.target.value = '';
            }
        },

        _scanBarcode: function (barcode) {
            const self = this;
            rpc.query({
                model: 'stock.picking',
                method: 'on_barcode_scanned',
                args: [[this.recordData.id], barcode],
            }).then(function (result) {
                if (result && result.warning) {
                    self.displayNotification({
                        type: result.warning.title === 'Successfully Added' ? 'success' : 'warning',
                        title: result.warning.title,
                        message: result.warning.message,
                        sticky: false
                    });
                    if (result.warning.title === 'Successfully Added') {
                        $('body').append('<audio src="/f_delivery_barcode_scan/static/src/sounds/success.wav" autoplay="true"></audio>');
                    }
                }
            }).catch(function (err) {
                console.error("Barcode Scan Error:", err);
            });
        },
    });

    fieldRegistry.add('barcode_handler', BarcodeField);
});
