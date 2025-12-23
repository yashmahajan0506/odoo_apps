import { Component, useState } from "@odoo/owl";

export class CounterWidget extends Component {
    static template = "sales_dashboard.CounterWidget";
    static props = {
        value: { type: Number },
        onChange: { type: Function },
    };

    setup() {
        this.state = useState({
            value: this.props.value || 0,
        });
    }

    increment() {
        this.state.value++;
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }

    decrement() {
        this.state.value--;
        if (this.props.onChange) {
            this.props.onChange(this.state.value);
        }
    }
}
