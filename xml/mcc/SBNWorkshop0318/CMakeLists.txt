FILE(GLOB xml_files *.xml)
install(FILES ${xml_files} DESTINATION xml/mcc/SBNWorkshop1017)
install_source( EXTRAS ${xml_files} )
