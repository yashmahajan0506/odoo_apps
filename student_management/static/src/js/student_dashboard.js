import { Component, useState, onMounted } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";


export class StudentDashboard extends Component {
    setup() 
    {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            total_students: 0,
            active_students: 0,
            male_students:0,
            female_students:0,
            department_count : 0,
            subject_count: 0,
        });

        onMounted(() => {
            this.loadData().then(() => this.renderCharts());
        });
    }

    async loadData() {
        const result = await this.orm.searchRead(
            "student.dashboard",
            [],
            ["total_students", "active_students", "department_count", "subject_count","male_students","female_students"]
        );

        if (result.length) {
            Object.assign(this.state, result[0]);
        }
    }

openStudentList(ev, filter) {
    if (ev && ev.stopPropagation) {
        ev.stopPropagation();
    }

    let actionConfig = {
        name: "Records",
        type: "ir.actions.act_window",
        views: [
            [false, "list"],
            [false, "form"]
        ],
        view_mode: "list,form",
        domain: [],
        res_model: null,   
    };

    if (filter === "active") {
        actionConfig.res_model = "student.student";
        actionConfig.domain = [["is_active", "=", true]];
    }
    else if (filter === "male") {
        actionConfig.res_model = "student.student";
        actionConfig.domain = [["gender", "=", "male"]];
    }
    else if (filter === "female") {
        actionConfig.res_model = "student.student";
        actionConfig.domain = [["gender", "=", "female"]];
    }

    else if (filter === "department") {
        actionConfig.name = "Departments";
        actionConfig.res_model = "school.department";
    }

  
    else if (filter === "subject") {
        actionConfig.name = "Subjects";
        actionConfig.res_model = "school.subject";
    }

    if (!actionConfig.res_model) {
        console.error("Invalid filter passed:", filter);
        return;  
    }

    this.action.doAction(actionConfig);
}
addStudent() {
    this.action.doAction({
        type: 'ir.actions.act_window',
        name: 'Add Student',
        res_model: 'student.student',
        view_mode: 'form',
        views: [[false, "form"]],
        target: 'current',
    });
}

addDepartment() {
    this.action.doAction({
        type: 'ir.actions.act_window',
        name: 'Add Department',
        res_model: 'school.department',  
        view_mode: 'form',
        views: [[false, "form"]],
        target: 'current',
    });
}

addSubject() {
    this.action.doAction({
        type: 'ir.actions.act_window',
        name: 'Add Subject',
        res_model: 'school.subject',    
        view_mode: 'form',
        views: [[false, "form"]],
        target: 'current',
    });
}

async downloadDashboardPDF() {
    const pdf_data = await this.orm.call(
        "student.dashboard", 
        "generate_pdf",           
        []                       
    );

    const link = document.createElement("a");
    link.href = "data:application/pdf;base64," + pdf_data.pdf_base64;
    link.download = "student_dashboard.pdf";
    link.click();
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
