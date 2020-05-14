import * as constants from "./constants";

export function create_action(action) {
    switch(action.action_type) {
        case 'toggle_panel':
            return {
                type: constants.TOGGLE_PANEL,
                ref: action.ref,
            };
        case 'collapse_panel':
            return {
                type: constants.COLLAPSE_PANEL,
                ref: action.ref,
            };
        case 'set_value':
            return {
                type: constants.SET_VALUE,
                name: action.name,
                value: action.value,
            }
        case 'remove_value':
            return {
                type: constants.REMOVE_VALUE,
                name: action.name,
                value: action.value,
            }
        case 'submit_form':
            return {
                type: constants.SUBMIT_FORM,
            };
        case 'clear_search_input':
            return {
                type: constants.CLEAR_SEARCH_INPUT,
            };
        case 'link':
            return {
                type: constants.LINK,
                url: action.url,
            };
        default:
            console.error('Unknown action type', action);
            throw new Error(`Unknown action ${action.action_type}`);
    }
}