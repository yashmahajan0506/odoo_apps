import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class StudentDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            total_students: 0,
            active_students: 0,
            male_students: 0,
            female_students: 0,
        });

        onMounted(() => {
            this.loadData().then(() => this.renderCharts());
        });
    }

    async loadData() {
        const result = await this.orm.searchRead(
            "student.dashboard",
            [],
            ["total_students", "active_students", "male_students", "female_students"]
        );

        if (result.length) {
            Object.assign(this.state, result[0]);
        }
    }


    openStudentList(ev, filter) {
        if (ev && ev.stopPropagation) {
            ev.stopPropagation();
        }

        let domain = [];

        if (filter === "active") {
            domain = [["is_active", "=", true]];
        } else if (filter === "male") {
            domain = [["gender", "=", "male"]];
        } else if (filter === "female") {
            domain = [["gender", "=", "female"]];
        }

        this.action.doAction({
            name: "Student List",
            type: "ir.actions.act_window",
            res_model: "student.student",
              views: [
            [false, "list"],
            [false, "form"]
        ],
            view_mode: "list,form",
            domain: domain,
        });
    }


    renderCharts() {
        const state = this.state;

        new Chart(document.getElementById("pieChart"), {
            type: "pie",
            data: {
                labels: ["Male", "Female"],
                datasets: [{
                    data: [state.male_students, state.female_students],
                    backgroundColor: ["#6a89ff", "#ff6fa8"],
                }],
            }
        });

        new Chart(document.getElementById("barChart"), {
            type: "bar",
            data: {
                labels: ["Total", "Active"],
                datasets: [{
                    data: [state.total_students, state.active_students],
                    backgroundColor: ["#55efc4", "#74b9ff"],
                }],
            },
            options: { plugins: { legend: { display: false } } }
        });
    }
}

StudentDashboard.template = "student_management.StudentDashboardMain";

registry.category("actions").add("student_dashboard_action_js", StudentDashboard);
