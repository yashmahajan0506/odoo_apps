import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

export class AttachmentPreviewDialog extends Component {
    static components = { Dialog };
    static template = "sales_dashboard.AttachmentPreviewDialog";

    static props = {
        close: Function,
        attachments: Array,
    };

    get attachments() {
        return this.props.attachments || [];
    }
    // get attachmentcount(){
    //     return this.attachments.length;
    // }
}

export class AttachmentPreviewField extends Component {
    static template = "sales_dashboard.AttachmentPreviewField";
    static props = {
        ...standardFieldProps,
    };

    setup() {
        this.dialog = useService("dialog");
        this.orm = useService("orm");
    }

    async onPreview() {
        const fieldData = this.props.record.data[this.props.name];
        let attachmentIds = [];

        if (fieldData && fieldData.records) {
            attachmentIds = fieldData.records.map(r => r.resId).filter(id => id);
        }

        if (attachmentIds.length === 0) return;

        const attachments = await this.orm.read("ir.attachment", attachmentIds, ["name", "mimetype"]);

        this.dialog.add(AttachmentPreviewDialog, {
            attachments: attachments,
        });
    }

    get hasAttachments() {
        const fieldData = this.props.record.data[this.props.name];
        return fieldData && fieldData.records && fieldData.records.length > 0;
    }
}

export const attachmentPreviewField = {
    component: AttachmentPreviewField,
};

registry.category("fields").add("attachment_preview", attachmentPreviewField);


