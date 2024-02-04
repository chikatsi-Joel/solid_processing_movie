interface cloud_provider {
    public void  storeFile();
    public void getFile(String name);
    public void createServer(String region);
    public void listServer(String region);
    public void getCDNAdress();
}

interface FileStorage {
    void storeFile();
    void getFile(String name);
}

interface ServerManagement {
    void createServer(String region);
    void listServer(String region);
}

interface CDNManagement {
    void getCDNAddress();
}


class Amazon implements cloud_provider{
    @Override public void  storeFile() {

    }
    @Override public void getFile(String name) {

    }
    @Override public void createServer(String region){

    }
    @Override public void listServer(String region){

    }
    @Override public void getCDNAdress(){

    }
}

class DropBox implements cloud_provider {
    @Override public void  storeFile() {

    }
    @Override public void getFile(String name) {

    }
    @Override public void createServer(String region){

    }
    @Override public void listServer(String region){
        throw new AbstractMethodError();
    }
    @Override public void getCDNAdress(){
        throw new AbstractMethodError();
    }
}

