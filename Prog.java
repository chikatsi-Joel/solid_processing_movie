import java.util.List;


abstract class Document {
    private String data;
    private String filename;

    public void open() {

    }
    public abstract void save();
}

class ReadOnly extends Document {
    @Override public void save () {
        throw new AbstractMethodError();
    }
}   

class modifiable extends Document{
    @Override public void save () {

    }
}


class Project {
    List<Document> documents;

    public void openALl() {
        documents.stream().forEach(Document::open);
    }

    public void saveAll() {
        documents.stream().forEach(Document::save);
    }
}