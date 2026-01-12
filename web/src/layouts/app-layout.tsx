import { useEffect, useState } from "react";
import { Outlet } from "react-router";
import { Box, ActionIcon } from "@mantine/core";
import { useMediaQuery } from "@mantine/hooks";
import AppSidebar, { SidebarToggle } from "@/components/app-sidebar";

const SIDEBAR_STORAGE_KEY = "sidebar-opened";

function getInitialSidebarState(): boolean {
    if (typeof window === "undefined") return true;
    
    // Check if mobile on initial load to prevent flash
    const isMobileInitial = window.innerWidth < 768;
    
    // On mobile, always start closed to prevent flash
    if (isMobileInitial) return false;
    
    // On desktop, check localStorage
    const stored = localStorage.getItem(SIDEBAR_STORAGE_KEY);
    return stored !== null ? stored === "true" : true;
}

export default function AppLayout() {
    const isMobile = useMediaQuery("(max-width: 767px)");
    const [opened, setOpened] = useState(() => getInitialSidebarState());

    // Update sidebar state based on screen size
    useEffect(() => {
        if (isMobile) {
            setOpened(false);
        } else {
            // On desktop, restore from localStorage or default to true
            const stored = localStorage.getItem(SIDEBAR_STORAGE_KEY);
            setOpened(stored !== null ? stored === "true" : true);
        }
    }, [isMobile]);

    // Save to localStorage when opened state changes (only on desktop)
    useEffect(() => {
        if (!isMobile) {
            localStorage.setItem(SIDEBAR_STORAGE_KEY, opened.toString());
        }
    }, [opened, isMobile]);

    const toggle = () => {
        setOpened((prev) => !prev);
    };

    return (
        <Box style={{ minHeight: "100vh" }}>
            {/* Toggle Button - Mobile */}
            <ActionIcon
                variant="subtle"
                onClick={toggle}
                size="lg"
                style={{
                    position: "fixed",
                    top: "1rem",
                    left: "1rem",
                    zIndex: 200,
                }}
                hiddenFrom="sm"
            >
                ☰
            </ActionIcon>

            {/* Toggle Button - Desktop */}
            <SidebarToggle opened={opened} toggle={toggle} />

            {/* Sidebar */}
            <AppSidebar opened={opened} toggle={toggle} />

            {/* Main Content */}
            <Box
                style={{
                    padding: "2rem",
                    paddingTop: "4rem",
                    minHeight: "100vh",
                    marginLeft: opened ? "280px" : "0",
                    transition: "margin-left 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
                    position: "relative",
                    zIndex: 1,
                }}
                visibleFrom="sm"
            >
                <Box
                    style={{
                        maxWidth: "1200px",
                        margin: "0 auto",
                    }}
                >
                    <Outlet />
                </Box>
            </Box>
            <Box
                style={{
                    padding: "1rem",
                    paddingTop: "4rem",
                    minHeight: "100vh",
                }}
                hiddenFrom="sm"
            >
                <Outlet />
            </Box>
        </Box>
    );
}
