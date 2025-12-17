import { Component, useState } from "@odoo/owl";

export class CounterWidget extends Component {
    setup() {
        this.state = useState({
            value: this.props.value || 0,
        });
    }

    increment() {
        this.state.value++;
        this.props.onChange?.(this.state.value);
    }

    decrement() {
        if (this.state.value > 0) {
            this.state.value--;
            this.props.onChange?.(this.state.value);
        }
    }
}

CounterWidget.template = "sales_dashboard.CounterWidget";
