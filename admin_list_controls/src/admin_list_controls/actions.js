import {TOGGLE_PANEL} from "./constants";

export function create_action(action) {
    switch(action.action_type) {
        case 'toggle_panel':
            return {
                type: TOGGLE_PANEL,
                ref: action.ref,
            };
        case 'set_value':
        case 'append_value':
        case 'remove_value':
        case 'link':
        case 'submit_form':
        default:
            console.error('Unknown action type', action);
            throw new Error(`Unknown action ${action.action_type}`);
    }
}