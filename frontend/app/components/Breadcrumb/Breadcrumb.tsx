import Link from 'next/link';
import styles from './Breadcrumb.module.css';

type BreadcrumbItem = {
    label: string;
    href?: string;
    icon?: React.ReactNode;
};

type BreadcrumbProps = {
    items: BreadcrumbItem[];
};

export default function Breadcrumb({ items }: BreadcrumbProps) {
    return (
        <nav aria-label="Breadcrumb" className={styles.nav}>
            {items.map((item, index) => {
                const isActive = index === items.length - 1;
                const content = (
                    <>
                        {item.icon && <span className={styles.itemIcon}>{item.icon}</span>}
                        <span>{item.label}</span>
                    </>
                );

                return (
                    <div
                        key={index}
                        className={[styles.item, isActive ? styles.active : styles.previous].join(' ')}
                        style={index > 0 ? { marginLeft: '3px' } : undefined}
                        aria-current={isActive ? 'page' : undefined}
                    >
                        {!isActive && item.href ? (
                            <Link href={item.href} className={styles.link}>
                                {content}
                            </Link>
                        ) : (
                            <span className={styles.link}>{content}</span>
                        )}
                    </div>
                );
            })}
        </nav>
    );
}
