import {ListControls} from "./list_controls";
import {Button} from "./button";
import {Panel} from "./panel";
import {Icon} from "./icon";
import {Text} from "./text";
import {Divider} from "./divider";
import {Block} from "./block";

export function render_control(control) {
    switch (control.object_type) {
        case 'list_controls':
            return <ListControls control={control}/>;
        case 'button':
            return <Button control={control}/>;
        case 'panel':
            return <Panel control={control}/>;
        case 'icon':
            return <Icon control={control}/>;
        case 'text':
            return <Text control={control}/>;
        case 'divider':
            return <Divider control={control}/>;
        case 'block':
            return <Block control={control}/>;
        default:
            console.error('Unknown control type', control);
            throw new Error(`Unknown control ${control.object_type}`);
    }
}