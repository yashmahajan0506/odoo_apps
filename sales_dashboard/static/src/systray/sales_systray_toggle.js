/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { CustomSaleSmartFilter } from "../js/custom_sale_smart_filter";

export class SalesSystraySearch extends Component {
    setup() {
        this.dialog = useService("dialog");
        this.action = useService("action");
    }

    openSearchPanel() {
        const closeDialog = this.dialog.add(CustomSaleSmartFilter, {
            title: "Sales Smart Search",
            isDialog: true,
            liveSearch: false,
            onFilterChange: this.onSearch.bind(this, () => closeDialog()),
        });
    }

    onSearch(close, data) {
        close();
        this.action.doAction("sales_dashboard.sales_dashboard_action", {
            options: {
                clear_breadcrumbs: true,
            },
            additional_context: {
                default_search_query: data.search,
                default_filter: data.filter,
            },
        });
    }
}

SalesSystraySearch.template =
    "sales_dashboard.SalesSystraySearch";

registry.category("systray").add(
    "sales_dashboard.systray_search",
    {
        Component: SalesSystraySearch,
        sequence: 80,
    }
);
