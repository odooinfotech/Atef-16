/** @odoo-module **/

import BarcodeModel from '@stock_barcode/models/barcode_model';
import { patch } from 'web.utils';

patch(BarcodeModel.prototype, 'barcode_customization', {
    selectLine(line) {
        let sub_line = false;
        if (line && line.product_id.tracking !== 'none' && line.product_id.is_scan_by_lot) {
            if(line && line.lines && line.lines.length > 0 && this.selectedLineVirtualId){
                sub_line = line.lines.find(l =>  l.virtual_id == this.selectedLineVirtualId);
            }
        }
        // Added below condition as when user tries to click on the grouped line, when the
        // subline of any other group is open then we need to pass the group line itself.
        if (sub_line){
            this._super(sub_line)
        }else{
            this._super(line)
        }
    },
    /**
     * Starts by parse the barcode and then process each type of barcode data.
     *
     * @param {string} barcode
     * @returns {Promise}
     */
    async _processBarcode(barcode) {
        if (this.selectedLine && this.selectedLine.lot_id && this.selectedLine.product_id.tracking !== 'none' && this.selectedLine.product_id.is_scan_by_lot) {
            if (this.selectedLine.product_id.barcode === barcode){
                barcode = this.selectedLine.lot_id.name
            }
        }
        await this._super(barcode)
    }
});
