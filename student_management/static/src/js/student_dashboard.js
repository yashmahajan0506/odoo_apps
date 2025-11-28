import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class StudentDashboard extends Component {
    setup() {
        this.orm = useService("orm");

        this.state = useState({
            total_students: 0,
            active_students: 0,
            male_students: 0,
            female_students: 0,
        });

        onMounted(() => this.loadData());
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
}

StudentDashboard.template = "student_management.StudentDashboardMain";

registry.category("actions").add("student_dashboard_action_js", StudentDashboard);
