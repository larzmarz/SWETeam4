const database = 'users';
const collection = 'usernames';
const collection1 = 'passwords';

use(database);
db.createCollection(collection);
db.createCollection(collection1);
