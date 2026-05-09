"use client"
import { createContext, useState } from "react";

interface DataContextProp {
    isMenuMobileAberto: boolean,
    setIsMenuAbertoMobile: React.Dispatch<React.SetStateAction<boolean>>;
}

export const LayoutContext = createContext<DataContextProp | undefined>(undefined);

export function LayoutProvider({ children }: { children: React.ReactNode }) {
    const [isMenuMobileAberto, setIsMenuAbertoMobile] = useState(false);

    return(
        <LayoutContext.Provider value={{isMenuMobileAberto,setIsMenuAbertoMobile}}>
            {children}
        </LayoutContext.Provider>
    )
}

