import Checkbox from '../Checkbox/Checkbox';
import styles from './CheckboxList.module.css';

export type CheckboxItem = {
    id: string;
    label: string;
    sublabel?: string;
    disabled?: boolean;
};

type CheckboxListProps = {
    items: CheckboxItem[];
    selected: string[];
    onChange: (selected: string[]) => void;
    className?: string;
};

export default function CheckboxList({ items, selected, onChange, className }: CheckboxListProps) {
    function toggle(id: string) {
        if (selected.includes(id)) {
            onChange(selected.filter((s) => s !== id));
        } else {
            onChange([...selected, id]);
        }
    }

    return (
        <ul className={[styles.list, className ?? ''].filter(Boolean).join(' ')}>
            {items.map((item) => {
                const isChecked = selected.includes(item.id);
                return (
                    <li key={item.id} className={styles.item}>
                        <Checkbox
                            checked={isChecked}
                            onChange={() => toggle(item.id)}
                            disabled={item.disabled}
                        />
                        <span className={[styles.label, isChecked ? styles.labelChecked : ''].filter(Boolean).join(' ')}>
                            {item.label}
                        </span>
                        {item.sublabel && (
                            <span className={styles.sublabel}>{item.sublabel}</span>
                        )}
                    </li>
                );
            })}
        </ul>
    );
}
