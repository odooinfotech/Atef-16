/** @odoo-module **/

import { bus } from 'web.core';
import MainComponent from '@stock_barcode/components/main';
import { patch } from 'web.utils';

patch(MainComponent.prototype, 'FPrintPackages', {
    FPrintPackages(ev) {
        console.log("Start")
        ev.stopPropagation();
        this.env.model._FPrintPackages();
    }
});

patch(MainComponent.prototype, 'advancePutInPack', {
    advancePutInPack(ev) {
        console.log("Start")
        ev.stopPropagation();
        this.env.model._advancePutInPack();
    }
});
