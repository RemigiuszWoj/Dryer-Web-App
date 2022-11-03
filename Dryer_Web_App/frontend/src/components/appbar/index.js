import React, { Component } from "react";
import { useMediaQuery } from "@mui/material";
import { useTheme } from "@mui/material/styles";
import AppBarMobile from "./appbarMobile";
import AppBarDesktop from "./appbaDesktop";


export default function Appbar() {

    const theme = useTheme();
    const matches = useMediaQuery(theme.breakpoints.down("md"));


    return (
        <>
            {matches ? <AppBarMobile /> : <AppBarDesktop />}
        </>
        

    );
}