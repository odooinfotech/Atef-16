
/** @odoo-module **/
import BarcodeMain from '@stock_barcode/components/main';
import { patch } from 'web.utils';
import { _t } from 'web.core';
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
var Dialog = require('web.Dialog');


patch(BarcodeMain.prototype, 'validate', {
    async validate(ev) {
        ev.stopPropagation();
         Dialog.confirm(this, _t("by clicking on (Ok) Odoo will process This Inventory Adjustments."), {
            confirm_callback: () => {
               console.log("passsssss")
              this.env.model.validate();
            },
        });



        
      /*  this.env.services.dialog.add(ConfirmationDialog, { title, body: message });
        Dialog.confirm(this, _t("by clicking on (Ok) Odoo will process This Inventory Adjustments."), {
            confirm_callback: () => {
               console.log("passsssss")
               this.env.model.validate();

            },
        });*/
    }
});

