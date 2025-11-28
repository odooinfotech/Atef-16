
/** @odoo-module **/
import BarcodeQuantModel from '@stock_barcode/models/barcode_quant_model';
import { patch } from 'web.utils';
import { _t } from 'web.core';
var Dialog = require('web.Dialog');

const originalApply = BarcodeQuantModel.prototype.apply;

patch(BarcodeQuantModel.prototype, 'apply', {
    async apply(ev) {
        Dialog.confirm(this, _t("by clicking on (Ok) Odoo will process This Inventory Adjustments."), {
            confirm_callback: () => {
               console.log("passsssss")
                return originalApply.call(this, ev);
            },
        });
    }
});

