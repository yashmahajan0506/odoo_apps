import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { loadBundle } from "@web/core/assets";
import { CounterWidget } from "./counter_widget";
import { CustomSaleSmartFilter } from "./custom_sale_smart_filter";

export class SalesDashboard extends Component {
    static components = { CounterWidget, CustomSaleSmartFilter };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            total_orders: 0,
            confirmed_orders: 0,
            quotations: 0,
            total_amount: 0,
            theme: "light",
            searchQuery: "",
            activeFilter: "all",
        });

        onMounted(() => {
            this.loadData().then(() => this.renderCharts());
        });
    }

    // ----------------------------------------------------------
    // LOAD DATA
    // ----------------------------------------------------------
    async loadData() {
        // Check for context params from systray search
        const context = this.props.action && this.props.action.context;
        if (context) {
            if (context.default_search_query) {
                this.state.searchQuery = context.default_search_query;
            }
            if (context.default_filter) {
                this.state.activeFilter = context.default_filter;
            }
        }

        // If we have search params, perform search instead of plain load
        if (this.state.searchQuery || this.state.activeFilter !== 'all') {
            await this.performSearch();
            return;
        }

        try {
            const kpiData = await this.orm.call("sale.dashboard", "get_sales_data", []);
            if (kpiData) {
                Object.assign(this.state, kpiData);
            }
        } catch (error) {
            console.error("Error loading dashboard data:", error);
        }
    }

    // ----------------------------------------------------------
    // SEARCH + FILTER
    // ----------------------------------------------------------
    handleFilterUpdate(data) {
        this.state.searchQuery = data.search;
        this.state.activeFilter = data.filter;
        this.performSearch();
    }

    async performSearch() {
        const query = this.state.searchQuery.trim();
        const filter = this.state.activeFilter;

        try {
            const result = await this.orm.call("sale.dashboard", "search_orders", [query, filter]);
            if (result) {
                Object.assign(this.state, result);
                this.renderCharts();   // re-render charts dynamically
            }
        } catch (error) {
            console.error("Search error:", error);
        }
    }

    toggleTheme() {
        this.state.theme = this.state.theme === "light" ? "dark" : "light";
    }

    // ----------------------------------------------------------
    // CHARTS (same style as Student Dashboard)
    // ----------------------------------------------------------
    async renderCharts() {
        await loadBundle("web.chartjs_lib");
        const state = this.state;

        // PIE CHART
        new Chart(document.getElementById("salesPieChart"), {
            type: "pie",
            data: {
                labels: ["Confirmed Orders", "Quotations"],
                datasets: [
                    {
                        data: [state.confirmed_orders, state.quotations],
                        backgroundColor: ["#6a89ff", "#ff6fa8"],
                    },
                ],
            },
        });

        // BAR CHART
        new Chart(document.getElementById("salesBarChart"), {
            type: "bar",
            data: {
                labels: ["Total Orders", "Total Amount"],
                datasets: [
                    {
                        data: [state.total_orders, state.total_amount],
                        backgroundColor: ["#55efc4", "#74b9ff"],
                    },
                ],
            },
            options: { plugins: { legend: { display: false } } }
        });
    }
}

SalesDashboard.template = "sales_dashboard.SalesDashboardMain";
registry.category("actions").add("sales_dashboard", SalesDashboard);
