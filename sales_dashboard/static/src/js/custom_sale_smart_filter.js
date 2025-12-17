import { Component, useState } from "@odoo/owl";

export class CustomSaleSmartFilter extends Component {
    static template = "custom_sale_smart_filter.CustomSaleSmartFilter";
    static props = {
        onFilterChange: { type: Function, optional: true },
        isDialog: { type: Boolean, optional: true },
        liveSearch: { type: Boolean, optional: true },
        close: { type: Function, optional: true },
        title: { type: String, optional: true },
    };

    static defaultProps = {
        liveSearch: true,
    };

    setup() {
        this.state = useState({
            search: "",
            activeFilter: "all",
            isPanelVisible: this.props.isDialog || false,
        });
    }

    onFocus() {
        this.state.isPanelVisible = true;
    }

    closePanel() {
        this.state.isPanelVisible = false;
    }

    onSearchInput(ev) {
        this.state.search = ev.target.value;
        if (this.props.liveSearch) {
            this.notifyChange();
        }
    }

    onKeyDown(ev) {
        if (ev.key === "Enter") {
            this.notifyChange();
        }
    }

    setFilter(key) {
        this.state.activeFilter = key;
        this.notifyChange();
    }

    notifyChange() {
        if (this.props.onFilterChange) {
            this.props.onFilterChange({
                search: this.state.search,
                filter: this.state.activeFilter
            });
        }
    }
}
