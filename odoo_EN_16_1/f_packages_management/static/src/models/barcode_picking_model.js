/** @odoo-module **/

import BarcodePickingModel from '@stock_barcode/models/barcode_picking_model';
import { patch } from 'web.utils';
import { _t } from 'web.core';


patch(BarcodePickingModel.prototype, '_FPrintPackages', {
    async _FPrintPackages() {
        if (!this.groups.group_tracking_lot) {
            return this.notification.add(
                _t("To use packages, enable 'Packages' in the settings"),
                { type: 'danger'}
            );
        }
        await this.save();
        console.log("Call")
        const result = await this.orm.call(
            this.params.model,
            'f_print_packages',
            [[this.params.id]]
        );
        console.log("End Call")
        if (result) {
            console.log("result")
            this.trigger('process-action', result);
            console.log("result2")
        } else {
            console.log("fail result")
            this.trigger('refresh');
            console.log("fail result2")
        }
        console.log("end")
    }

});
patch(BarcodePickingModel.prototype, '_advancePutInPack', {
    async _advancePutInPack() {
        if (!this.groups.group_tracking_lot) {
            return this.notification.add(
                _t("To use packages, enable 'Packages' in the settings"),
                { type: 'danger'}
            );
        }
        await this.save();
        console.log("Call")
        const result = await this.orm.call(
            this.params.model,
            'f_action_put_in_pack',
            [[this.params.id]]
        );
        console.log("End Call")
        if (result === 'object') {
            this.trigger('process-action', result);
        } else {
            this.trigger('refresh');
        }
        console.log("end")
    }

});
